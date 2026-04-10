# Spring Controller and Service Generation

Generate a REST controller and its companion service class for the target Spring Boot application.

## Shared Rules (Service and Controller)

- Use **constructor injection** with `@Autowired`. Never field injection.
- Return **DTOs** from all methods — never expose JPA entities directly.
- Add necessary imports for `Entity`, `DTO`, and `Repository` classes.

```java
// Constructor injection pattern
@Autowired
public MyService(MyRepository myRepository) {
    this.myRepository = myRepository;
}
```

## Service Rules

- Annotate the class with `@Service`.
- Identify the service methods needed by examining each controller action:
  - `save` and `delete` operations are already provided by Spring Data JPA repositories — do not re-implement them in the service unless additional logic is needed.
  - Focus on query and transformation methods.
- Do **not** use mappers for data conversion. Return DTOs directly from repository query methods.
- Ensure every method's return type is a DTO (or `List<DTO>`, `Optional<DTO>`, etc.).

```java
@Service
public class CountryService {
    private final CountryEORepository countryEORepository;

    @Autowired
    public CountryService(CountryEORepository countryEORepository) {
        this.countryEORepository = countryEORepository;
    }

    public List<CountryDTO> getAllCountries() {
        return countryEORepository.findAllCountries();
    }
}
```

## Controller Rules

- Annotate the class with `@RestController` and `@RequestMapping("/api/...")`.
- Ensure all methods have correct `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` annotations with the right path variables.
- Use `@PathVariable` for dynamic path segments and `@RequestParam` for query parameters.
- Apply type-conversion annotations on parameters when needed:

```java
@GetMapping("/changes")
public List<ChangeDTO> getChanges(
    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date,
    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime time) {
    return changeService.findChanges(date, time);
}
```

- All return types must be DTOs or collections of DTOs.

```java
@RestController
@RequestMapping("/api/countries")
public class CountryController {
    private final CountryService countryService;

    @Autowired
    public CountryController(CountryService countryService) {
        this.countryService = countryService;
    }

    @GetMapping
    public List<CountryDTO> getAllCountries() {
        return countryService.getAllCountries();
    }
}
```

## Validation Checklist

- [ ] Constructor injection used everywhere (no `@Autowired` on fields)
- [ ] All return types are DTOs — no entity types exposed
- [ ] `@DateTimeFormat` on `LocalDate`/`LocalDateTime` parameters
- [ ] All necessary imports present (`Entity`, `DTO`, `Repository`, `Service`)
- [ ] No mapper usage for data conversion

---

## ADF Source Notes (skip if not migrating from ADF)

When the source is an ADF `ViewImpl` / `ApplicationModuleImpl`:

- Review all **actions** and **action methods** in the ViewImpl to identify what service methods are needed.
- Identify which repository operations satisfy each action (findAll, findBy*, save, delete).
- The `SearchRegion` in the ViewImpl defines filter parameters — these become controller query parameters mapped to service method arguments.
- Map `SearchRegion` bind variables directly to `@RequestParam` values in the controller.
