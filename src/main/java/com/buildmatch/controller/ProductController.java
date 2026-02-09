package com.buildmatch.controller;

import com.buildmatch.model.Product;
import com.buildmatch.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
@CrossOrigin(origins = "*")
public class ProductController {

    @Autowired
    private ProductRepository productRepository;

    @GetMapping
    public List<Product> listAll() {
        return productRepository.findAll();
    }

    @GetMapping("/search")
    public List<Product> search(@RequestParam String name) {
        return productRepository.findByNameContainingIgnoreCase(name);
    }

    @GetMapping("/category/{category}")
    public List<Product> listByCategory(@PathVariable String category) {
        return productRepository.findByCategory(category);
    }

    @GetMapping("/search")
    public List<Product> search(@RequestParam String q) {
        return productRepository.findByNameContainingIgnoreCase(q);
    }

    @PostMapping
    public Product create(@RequestBody Product product) {
        return productRepository.save(product);
    }
}
