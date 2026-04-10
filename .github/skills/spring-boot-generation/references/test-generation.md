# Spring Boot Test Generation

This file covers three test types. Read the relevant section for your task.

---

## Unit Tests {#unit-tests}

Generate unit tests for a Spring service using Mockito and JUnit 5.

### Rules

- Use only `@ExtendWith(MockitoExtension.class)` as the class-level annotation. No other Spring context annotations.
- Annotate the class field for the system under test with `@InjectMocks`.
- Annotate each dependency with `@Mock`.
- Mock the repository to return DTOs directly (don't go through entity→DTO mapping in unit tests).
- Use the provided SQL or test data as dummy objects in `@BeforeEach`.
- Give tests insightful names that describe behavior and expectation — readers should understand the test from the name alone.
- Use `when(...).thenReturn(...)` for stubbing. Use **`lenient().when(...)...`** for stubs in `@BeforeEach` that are not used in every test method — this avoids UnnecessaryStubbingException.
- Review whether any stubs are only needed in some test methods; if so, move them to those specific tests rather than keeping them in `@BeforeEach`.
- Use AssertJ (`assertThat`, `assertNotNull`, `assertEquals`, `assertTrue`) for assertions — not raw JUnit asserts.
- Include all necessary imports and the package declaration.

### Example

```java
@ExtendWith(MockitoExtension.class)
public class CountryServiceTest {

    @Mock
    private CountryEORepository countryEORepository;

    @InjectMocks
    private CountryService countryService;

    private CountryDTO country1, country2;

    @BeforeEach
    void setUp() {
        country1 = new CountryDTO(1, "USA", 1, "US");
        country2 = new CountryDTO(2, "Canada", 1, "CA");

        lenient().when(countryEORepository.findAllCountries())
                 .thenReturn(Arrays.asList(country1, country2));
    }

    @Test
    void getAllCountries_ShouldReturnListOfCountryDTOs_WhenDataIsAvailable() {
        List<CountryDTO> countries = countryService.getAllCountries();

        assertNotNull(countries);
        assertEquals(2, countries.size());
        assertEquals("USA", countries.get(0).getCountry());
    }

    @Test
    void getAllCountries_ShouldReturnEmptyList_WhenNoDataIsAvailable() {
        when(countryEORepository.findAllCountries()).thenReturn(Collections.emptyList());
        assertTrue(countryService.getAllCountries().isEmpty());
    }
}
```

---

## MVC Tests {#mvc-tests}

Generate controller tests using Spring MVC Test (`@WebMvcTest`).

### Rules

- Use `@WebMvcTest(MyController.class)` — loads only the MVC layer, not the full application context.
- Inject `MockMvc` with `@Autowired`.
- Use `@MockBean` to inject services (Spring manages the mock lifecycle in this context).
- Use the provided SQL / test data as sample DTOs in `@BeforeEach`.
- Ensure attribute types in test data match the DTO field types exactly.
- Name tests descriptively so behavior and expectation are clear at a glance.

### Example

```java
@WebMvcTest(CountryController.class)
public class CountryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private CountryService countryService;

    private List<CountryDTO> countryList;

    @BeforeEach
    public void setUp() {
        CountryDTO country1 = new CountryDTO(1, "Brazil", 2, "BR");
        CountryDTO country2 = new CountryDTO(2, "Japan", 4, "JP");
        countryList = Arrays.asList(country1, country2);
    }

    @Test
    public void testGetAllCountries_ReturnsOkWithCountryList() throws Exception {
        Mockito.when(countryService.getAllCountries()).thenReturn(countryList);

        mockMvc.perform(get("/api/countries")
                        .contentType(MediaType.APPLICATION_JSON))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$", hasSize(2)))
               .andExpect(jsonPath("$[0].country", is("Brazil")))
               .andExpect(jsonPath("$[1].country", is("Japan")));
    }
}
```

---

## Integration Tests {#integration-tests}

Generate repository integration tests using `@DataJpaTest`.

### Rules

- Annotate with `@DataJpaTest` and `@DisplayName("...")`.
- Extend `BaseRepositoryTest` — assume this class exists and provides all database configuration. **Do not add any additional configuration.**
- Inject the repository under test with `@Autowired`.
- Each test method is annotated with `@Test` and `@DirtiesContext`. No other configuration annotations on individual tests.
- Create specific, data-driven assertions using the actual SQL test data (provided as fixtures). The number of `INSERT` statements in the SQL fixture directly indicates the expected row count.
- Ensure the code compiles — perform a mental compile simulation before finalizing.

### Example

```java
@DataJpaTest
@DisplayName("Country repository tests.")
public class CountryEORepositoryIntegrationTest extends BaseRepositoryTest {

    @Autowired
    private CountryEORepository countryEORepository;

    @Test
    @DirtiesContext
    public void testFindAllCountryEOs() {
        // When
        List<CountryDTO> countries = countryEORepository.findAllCountries();

        // Then
        assertThat(countries).isNotEmpty();
        assertThat(countries).hasSize(14); // reflects INSERT count in test SQL
        assertThat(countries.get(0).getCountry()).isEqualTo("Brazil");
    }
}
```

### Validation Checklist

- [ ] No extra configuration annotations on the class or test methods
- [ ] `extends BaseRepositoryTest` present
- [ ] Every test has `@Test` and `@DirtiesContext`
- [ ] Assertions use actual values from the SQL test data
- [ ] `hasSize(N)` matches the number of INSERT rows in the fixture
