export type RequestMethods = "GET" | "POST" | "PUT" | "DELETE" | "HEAD";
export type Mode = "add" | "edit" | "view";

export interface Response {
  data: any;
  status: number;
}

export interface Request {
  method: RequestMethods;
  path: string;
  body?: Record<string, any>;
  multipart?: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface Store {
  id: string;
  name: string;
  slug: string;
  tables: Table[];
  categories: Category[]
}

export interface Product{
  id: string;
  name: string;
  slug: string;
}

export interface Category{
  id: string;
  name: string;
  slug: string;
  products: Product[]
}

export interface Table {
  id: string;
  name: string;
}

export interface Item {
  id: string;
  product: string;
  quantity: number,
  unit_price: number;
  amount: number
}

export interface Order {
    id: string;
    status: string;
    is_printed: boolean;
    created_at: string;
    updated_at: string;
    closed_at: string;
    table: Table;
    items: Item[],
    total: number;
  }