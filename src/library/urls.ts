import { BASE_URL } from "./settings";

interface URLRequirements {
  path: string;
  query?: Record<string, any>;
}

export function url(requirements: URLRequirements) {
  const url = new URL(requirements.path, BASE_URL);

  if (requirements.query) {
    Object.entries(requirements.query).forEach(([key, value]) => {
      url.searchParams.append(key, value);
    });
  }

  return url.toString();
}

export const urls = {
    csrf: url({ path: 'auth/csrf' }),
    check: url({ path: 'auth/check' }),
    logout: url({ path: 'auth/logout' }),
    login: url({ path: 'auth/login' }),
    order: url({ path: 'order' }),
    item: url({path: 'item'}),
    ticket: url({path: 'ticket'}),
}