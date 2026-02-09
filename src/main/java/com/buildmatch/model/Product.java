package com.buildmatch.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String category; // Ex: Materiais Brutos, Acabamentos, Estética
    private String supplier; // Ex: Leroy Merlin, Obramax, Tok&Stok
    private BigDecimal price;
    private String unit; // Ex: m2, kg, unidade
    private String link; // Link original do fornecedor
    private String imageUrl; // URL da imagem do produto
    
    private LocalDateTime lastUpdate;

    @PrePersist
    @PreUpdate
    public void onUpdate() {
        this.lastUpdate = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getSupplier() { return supplier; }
    public void setSupplier(String supplier) { this.supplier = supplier; }
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    public String getUnit() { return unit; }
    public void setUnit(String unit) { this.unit = unit; }
    public String getLink() { return link; }
    public void setLink(String link) { this.link = link; }
    public String getImageUrl() { return imageUrl; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    public LocalDateTime getLastUpdate() { return lastUpdate; }
    public void setLastUpdate(LocalDateTime lastUpdate) { this.lastUpdate = lastUpdate; }
}
