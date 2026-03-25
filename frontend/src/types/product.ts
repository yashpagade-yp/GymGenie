export interface Product {
  id: string;
  gym_id: string;
  name: string;
  description: string;
  price: string;
  image_url: string | null;
  in_stock: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductPayload {
  name: string;
  description: string;
  price: number;
  image_url?: string | null;
  in_stock?: boolean;
}
