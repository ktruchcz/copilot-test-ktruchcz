package com.example.testapp.controller;

import com.example.testapp.dto.ItemRequest;
import com.example.testapp.dto.ItemResponse;
import com.example.testapp.dto.StatusUpdateRequest;
import com.example.testapp.service.ItemService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/items")
@RequiredArgsConstructor
public class ItemController {

    private final ItemService itemService;

    @GetMapping
    public ResponseEntity<List<ItemResponse>> getAllItems() {
        return ResponseEntity.ok(itemService.getAllItems());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ItemResponse> getItemById(@PathVariable Long id) {
        return ResponseEntity.ok(itemService.getItemById(id));
    }

    @PostMapping
    public ResponseEntity<ItemResponse> createItem(@Valid @RequestBody ItemRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(itemService.createItem(request));
    }

    @PutMapping("/{id}")
    public ResponseEntity<ItemResponse> updateItem(@PathVariable Long id,
                                                    @Valid @RequestBody ItemRequest request) {
        return ResponseEntity.ok(itemService.updateItem(id, request));
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<ItemResponse> updateItemStatus(@PathVariable Long id,
                                                          @Valid @RequestBody StatusUpdateRequest request) {
        return ResponseEntity.ok(itemService.updateItemStatus(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteItem(@PathVariable Long id) {
        itemService.deleteItem(id);
        return ResponseEntity.noContent().build();
    }
}
