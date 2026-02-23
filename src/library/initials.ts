import type { Category, LoginCredentials, Order, Store } from "./interface";

export const initialCredentials: LoginCredentials = {
  username: "UlasO",
  password: "Gu190582751",
};

export const initialCategory: Category = {
  id: "",
  name: "",
  slug: "",
  products: [],
};

export const initialStore: Store = {
  id: "",
  name: "",
  slug: "",
  tables: [],
  categories: [{ ...initialCategory }],
};

export const initialOrder: Order = {
  id: "",
  status: "OPEN",
  is_printed: false,
  created_at: "",
  updated_at: "",
  closed_at: "",
  table: {
    id: "",
    name: "",
  },
  items: [],
  total: 0.00
};
