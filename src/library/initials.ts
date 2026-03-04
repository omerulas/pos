import type {
  CartItem,
  Category,
  LoginCredentials,
  Order,
  Store,
} from "./interface";

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
  is_open: false,
  items: [],
  amount: 0.0,
  tickets: [],
  is_printed: false,
};
