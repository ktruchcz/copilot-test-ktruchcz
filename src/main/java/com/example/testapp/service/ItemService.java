package com.example.testapp.service;

import com.example.testapp.dto.ItemRequest;
import com.example.testapp.dto.ItemResponse;
import com.example.testapp.dto.StatusUpdateRequest;
import com.example.testapp.exception.InvalidStatusException;
import com.example.testapp.exception.ItemNotFoundException;
import com.example.testapp.model.Item;
import com.example.testapp.repository.ItemRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional
public class ItemService {

    private static final Set<String> VALID_STATUSES = Set.of("active", "inactive", "deleted");

    private final ItemRepository itemRepository;

    @Transactional(readOnly = true)
    public List<ItemResponse> getAllItems() {
        return itemRepository.findAll().stream()
                .map(ItemResponse::fromItem)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public ItemResponse getItemById(Long id) {
        Item item = itemRepository.findById(id)
                .orElseThrow(() -> new ItemNotFoundException(id));
        return ItemResponse.fromItem(item);
    }

    public ItemResponse createItem(ItemRequest request) {
        String status = (request.getStatus() != null && !request.getStatus().isBlank())
                ? request.getStatus() : "active";
        if (!VALID_STATUSES.contains(status)) {
            throw new InvalidStatusException(status);
        }
        Item item = Item.builder()
                .name(request.getName())
                .description(request.getDescription())
                .status(status)
                .build();
        Item saved = itemRepository.saveAndFlush(item);
        return ItemResponse.fromItem(saved);
    }

    public ItemResponse updateItem(Long id, ItemRequest request) {
        Item item = itemRepository.findById(id)
                .orElseThrow(() -> new ItemNotFoundException(id));

        if (request.getName() != null && !request.getName().isBlank()) {
            item.setName(request.getName());
        }
        if (request.getDescription() != null) {
            item.setDescription(request.getDescription());
        }
        if (request.getStatus() != null && !request.getStatus().isBlank()) {
            if (!VALID_STATUSES.contains(request.getStatus())) {
                throw new InvalidStatusException(request.getStatus());
            }
            item.setStatus(request.getStatus());
        }

        Item saved = itemRepository.saveAndFlush(item);
        return ItemResponse.fromItem(saved);
    }

    public ItemResponse updateItemStatus(Long id, StatusUpdateRequest request) {
        Item item = itemRepository.findById(id)
                .orElseThrow(() -> new ItemNotFoundException(id));

        String newStatus = request.getStatus();
        if (!VALID_STATUSES.contains(newStatus)) {
            throw new InvalidStatusException(newStatus);
        }

        item.setStatus(newStatus);
        Item saved = itemRepository.saveAndFlush(item);
        return ItemResponse.fromItem(saved);
    }

    public void deleteItem(Long id) {
        if (!itemRepository.existsById(id)) {
            throw new ItemNotFoundException(id);
        }
        itemRepository.deleteById(id);
    }
}
