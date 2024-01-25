package com.writerelief.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.writerelief.models.Letter;
import com.writerelief.repository.LetterRepository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;

/**
 * The service class, will be returning reactive types (Mono and Flux),
 * which are at the heart of the reactive programming model provided by Project
 * Reactor.
 * A Mono represents a stream of 0 to 1 elements, and Flux represents a stream
 * of 0 to N elements.
 */
@Service
public class LetterService {

    private final LetterRepository letterRepository;

    @Autowired // annotation is used in Spring to automatically inject the dependencies
               // required by your beans.
    public LetterService(LetterRepository letterRepository) {
        this.letterRepository = letterRepository;
    }

    // Saves a letter and returns a Mono that will emit the saved Letter once the
    // save operation completes
    public Mono<Letter> saveLetter(Mono<Letter> letterMono) {
        return letterMono.flatMap(letterRepository::save);
    }

    // Retrieves all letters as a Flux. Flux represents a sequence of 0..N items,
    // emitted asynchronously
    public Flux<Letter> getAllLetters() {
        return letterRepository.findAll();
    }

    // Additional service methods can be added as needed
}
