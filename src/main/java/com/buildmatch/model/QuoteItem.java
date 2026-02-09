package com.buildmatch.model;

import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "quote_items")
public class QuoteItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String supplier;
    private BigDecimal price;
    private String imageUrl;
    private String productLink;
    private String category;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getSupplier() { return supplier; }
    public void setSupplier(String supplier) { this.supplier = supplier; }
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    public String getImageUrl() { return imageUrl; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    public String getProductLink() { return productLink; }
    public void setProductLink(String productLink) { this.productLink = productLink; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
}
