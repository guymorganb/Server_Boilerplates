package com.writerelief.controller;

import org.springframework.web.bind.annotation.*;
import com.writerelief.models.Letter;
import com.writerelief.service.LetterService;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
/**
  Client
  │  
  │ (HTTP Request)
  ▼
Controller
  │  
  │ (Method call with params)
  ▼
Service
  │  
  │ (Business logic / Method call)
  ▼
Repository
  │  
  │ (Database operation)
  ▼
Model / Database
  │  
  │ (Results / Data)
  ▲
Repository
  │  
  │ (Processed data / Entities)
  ▲
Service
  │  
  │ (Optional additional processing)
  ▲
Controller
  │  
  │ (HTTP Response)
  ▲
Client
 */
@RestController
@RequestMapping("/letters")
public class LetterController {

    private final LetterService letterService;

    public LetterController(LetterService letterService) {
        this.letterService = letterService;
    }

    @PostMapping
    public Mono<ResponseEntity<Letter>> createLetter(@RequestBody Mono<Letter> letterMono) {
        return letterService
                .saveLetter(letterMono)
                .map(savedLetter -> ResponseEntity.status(HttpStatus.CREATED).body(savedLetter));
    }

    @GetMapping
    public Flux<Letter> getAllLetters() {
        return letterService.getAllLetters();
    }

    // You can add more endpoints to handle different CRUD operations
}