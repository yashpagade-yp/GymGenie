import type { Product } from "../../types/product";
import { formatCurrency } from "../../utils/formatters";

export function ProductPanel({ products }: { products: Product[] }) {
  return (
    <section className="panel-card member-product-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Counter Picks</p>
          <h2>Gym products</h2>
          <p className="muted">Browse what is available at your gym counter.</p>
        </div>
      </div>
      <div className="product-grid">
        {products.map((product) => (
          <article className="product-card" key={product.id}>
            <p className="eyebrow">{product.in_stock ? "In stock" : "Unavailable"}</p>
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <strong>{formatCurrency(product.price)}</strong>
          </article>
        ))}
      </div>
    </section>
  );
}
