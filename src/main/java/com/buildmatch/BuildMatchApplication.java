package com.buildmatch;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SpringBootApplication
public class BuildMatchApplication {
    private static final Logger logger = LoggerFactory.getLogger(BuildMatchApplication.class);

    public static void main(String[] args) {
        logger.info("Verificando variaveis de ambiente do Railway...");
        logger.info("PGHOST: {}", System.getenv("PGHOST"));
        logger.info("PGPORT: {}", System.getenv("PGPORT"));
        logger.info("PGDATABASE: {}", System.getenv("PGDATABASE"));
        logger.info("PGUSER: {}", System.getenv("PGUSER"));
        
        SpringApplication.run(BuildMatchApplication.class, args);
    }
}
