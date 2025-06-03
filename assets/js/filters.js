// Filter functionality for dataset accordion
document.addEventListener('DOMContentLoaded', function() {
    // Get all filter checkboxes
    const sectorFilters = document.querySelectorAll('input[name="sector"]');
    const granularityFilters = document.querySelectorAll('input[name="granularity"]');
    const clearButton = document.getElementById('clearFilters');
    const accordionItems = document.querySelectorAll('.accordion-item');
    const noResultsMessage = document.getElementById('noResults');
    
    // Add event listeners to all checkboxes
    sectorFilters.forEach(checkbox => {
        checkbox.addEventListener('change', filterDatasets);
    });
    
    granularityFilters.forEach(checkbox => {
        checkbox.addEventListener('change', filterDatasets);
    });
    
    // Clear filters button
    clearButton.addEventListener('click', function() {
        sectorFilters.forEach(checkbox => checkbox.checked = false);
        granularityFilters.forEach(checkbox => checkbox.checked = false);
        filterDatasets();
    });
    
    function filterDatasets() {
        // Get selected filters
        const selectedSectors = Array.from(sectorFilters)
            .filter(cb => cb.checked)
            .map(cb => cb.value.toLowerCase());
        
        const selectedGranularities = Array.from(granularityFilters)
            .filter(cb => cb.checked)
            .map(cb => cb.value.toLowerCase());
        
        let visibleCount = 0;
        
        // Filter accordion items
        accordionItems.forEach(item => {
            const sectors = item.dataset.sectors ? item.dataset.sectors.toLowerCase().split(',') : [];
            const granularity = item.dataset.granularity ? item.dataset.granularity.toLowerCase() : '';
            
            // Check if item matches filters
            const sectorMatch = selectedSectors.length === 0 || 
                sectors.some(sector => selectedSectors.includes(sector.trim()));
            
            const granularityMatch = selectedGranularities.length === 0 || 
                selectedGranularities.includes(granularity);
            
            if (sectorMatch && granularityMatch) {
                item.style.display = 'block';
                visibleCount++;
            } else {
                item.style.display = 'none';
                // Collapse hidden items
                const collapse = item.querySelector('.collapse');
                if (collapse && collapse.classList.contains('show')) {
                    $(collapse).collapse('hide');
                }
            }
        });
        
        // Show/hide no results message
        if (visibleCount === 0) {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }
    }
});