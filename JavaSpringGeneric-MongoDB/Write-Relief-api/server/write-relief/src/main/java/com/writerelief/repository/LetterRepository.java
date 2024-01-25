package com.writerelief.repository;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;
import com.writerelief.models.Letter;

/**
 * For the reactive repository, use ReactiveMongoRepository.
 * It returns Mono and Flux types from Project Reactor to work with the
 * asynchronous data flow.
 */
@Repository
public interface LetterRepository extends ReactiveMongoRepository<Letter, String> {
    // Custom query methods can be defined here
}