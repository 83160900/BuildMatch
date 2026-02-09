package com.buildmatch.controller;

import com.buildmatch.model.Quote;
import com.buildmatch.repository.QuoteRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// forced_rebuild: 20260209
@RestController
@RequestMapping("/api/quotes")
@CrossOrigin(origins = "*")
public class QuoteController {

    @Autowired
    private QuoteRepository quoteRepository;

    @GetMapping
    public List<Quote> list() {
        return quoteRepository.findAll();
    }

    @PostMapping
    public Quote create(@RequestBody Quote quote) {
        return quoteRepository.save(quote);
    }
    
    @GetMapping("/{id}")
    public Quote get(@PathVariable Long id) {
        return quoteRepository.findById(id).orElse(null);
    }
}
