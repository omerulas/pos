import Cookies from "js-cookie";
import type { Request, Response, RequestMethods } from "./interface.ts";
import useMessage from "@/stores/message.ts";
import { DEBUG } from "./settings";
import { useProcess } from "@/stores/process.ts";

enum HttpMethods {
  GET = "GET",
  POST = "POST",
  PUT = "PUT",
  DELETE = "DELETE",
  HEAD = "HEAD",
}

// services/api.service.ts
interface ApResponse<T = any> {
  data: T;
  status: number;
  message?: string;
  error?: string;
}

class ApiError extends Error {
  constructor(
    public message: string,
    public status: number,
    public data?: any,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

class ApiService {
  private static instance: ApiService;
  private defaultHeaders: HeadersInit = {
    Accept: "application/json",
  };

  // Singleton Pattern: Tek bir instance üzerinden yürümek bellek yönetimi için iyidir.
  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  /**
   * Headerları dinamik olarak oluşturur.
   * CSRF Token'ın her istekte güncel kalmasını sağlar.
   */
  private getHeaders(multipart: boolean = false): Headers {
    const headers = new Headers(this.defaultHeaders);
    const csrfToken = Cookies.get("csrftoken");

    if (csrfToken) {
      headers.append("X-CSRFToken", csrfToken);
    }

    // Multipart (Dosya yükleme) değilse Content-Type JSON olsun.
    // Multipart olduğunda tarayıcı "boundary"yi kendi ayarlar, o yüzden elle eklemiyoruz.
    if (!multipart) {
      headers.append("Content-Type", "application/json");
    }

    return headers;
  }

  /**
   * Gelen yanıt içinden kullanıcıya gösterilecek mesajı ayıklar.
   * Öncelik sırası: message -> error -> detail -> non_field_errors
   */
  private extractMessage(data: any): string | null {
    if (!data) return null;

    // 1. Standart "message" alanı
    if (data.message) return data.message;

    // 2. "error" alanı (Hem string hem obje olabilir)
    if (data.error) {
      if (typeof data.error === "string") return data.error;
      if (typeof data.error === "object" && data.error.message)
        return data.error.message;
    }

    // 3. Django Rest Framework standart hata alanı ("detail")
    if (data.detail) return data.detail;

    // 4. Django Form hataları (Genel hatalar)
    if (data.non_field_errors && Array.isArray(data.non_field_errors)) {
      return data.non_field_errors[0];
    }

    return null;
  }

  /**
   * Merkezi Request Yöneticisi
   * @param method HTTP Metodu
   * @param url İstek atılacak adres
   * @param body Gönderilecek veri
   * @param multipart Dosya yükleme durumu
   */
  private async request<T>(
    method: HttpMethods,
    url: string,
    body?: any,
    multipart: boolean = false,
  ): Promise<ApResponse<T>> {
    // Store'ları fonksiyon içinde çağırıyoruz ki circular dependency (döngüsel bağımlılık) olmasın.
    const processStore = useProcess();
    const messageStore = useMessage();

    // 1. Loading Başlat
    processStore.isLoading = true;

    // 2. Fetch Ayarları
    const config: RequestInit = {
      method,
      headers: this.getHeaders(multipart),
      credentials: "include", // Cookie paylaşımı için
    };

    if (body) {
      config.body = multipart ? body : JSON.stringify(body);
    }

    try {
      const response = await fetch(url, config);

      // 3. Yetki Kontrolü (401 / 403)
      if (response.status === 401) {
        processStore.isAuthenticated = false;
        // Opsiyonel: Login sayfasına yönlendir
        // window.location.href = '/login';
      }

      // 4. Yanıtı İşle (TEXT -> JSON dönüşümü ve Boş Yanıt Kontrolü)
      let data: any = {};

      // HEAD isteği veya 204 No Content ise body okumaya çalışma
      if (method !== HttpMethods.HEAD && response.status !== 204) {
        const text = await response.text();
        try {
          data = text ? JSON.parse(text) : {};
        } catch (err) {
          console.warn("JSON Parse Warning:", err);
          data = {}; // JSON değilse boş obje dön
        }
      }

      // 6. Global Mesaj Gösterimi (Akıllı Çıkarım)
      const userMessage = this.extractMessage(data);

      if (userMessage) {
        if (response.ok) {
          messageStore.add(userMessage);
        } else {
          // Store'unda error için ayrı bir metod varsa onu kullan, yoksa add kullan
          // messageStore.addError(userMessage);
          messageStore.add(userMessage);
        }
      }

      if (DEBUG) console.log(`[API] ${method} ${url}`, data);

      return {
        data: data.data as T,
        status: response.status,
      };
    } catch (error: any) {
      // Hata Yönetimi
      const status = error instanceof ApiError ? error.status : 500;
      const message = error.message || "Bilinmeyen bir hata oluştu";

      if (DEBUG) console.error(`[API Error] ${url}`, error);

      // İsteğe bağlı: Global hata mesajı bas
      // messageStore.addError(message);

      // Hatayı çağıran yere fırlatmayıp standart bir hata objesi de dönebiliriz,
      // ama "throw" etmek genellikle daha iyi bir pratiktir (try-catch kullanımı için).
      // Ancak senin mevcut yapına uygun olarak bir wrapper dönüyorum:
      return {
        data: (error.data || null) as T,
        status: status,
        message: message,
      };
    } finally {
      // 7. Loading Bitir
      processStore.isLoading = false;
    }
  }

  // --- Public Metodlar ---

  public get<T = any>(url: string): Promise<ApResponse<T>> {
    return this.request<T>(HttpMethods.GET, url);
  }

  public post<T = any>(
    url: string,
    body: any,
    multipart = false,
  ): Promise<ApResponse<T>> {
    return this.request<T>(HttpMethods.POST, url, body, multipart);
  }

  public put<T = any>(url: string, body: any): Promise<ApResponse<T>> {
    return this.request<T>(HttpMethods.PUT, url, body);
  }

  public delete<T = any>(url: string): Promise<ApResponse<T>> {
    return this.request<T>(HttpMethods.DELETE, url);
  }

  public head(url: string): Promise<ApResponse<void>> {
    return this.request<void>(HttpMethods.HEAD, url);
  }
}

// Kullanım kolaylığı için tek bir instance export ediyoruz
export const api = ApiService.getInstance();
