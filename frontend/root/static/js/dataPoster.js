// dataPoster.js
class DataPoster {
    constructor(loader, renderer, options = {}) {
        this.loader = loader;          // DataLoader instance
        this.renderer = renderer;      // ItemRenderer instance
        this.options = {
            formId: 'create-form',
            fieldMappings: {},        // Custom field mappings
            transformData: null,      // Optional data transformer
            beforeSubmit: null,       // Pre-submit hook
            afterSuccess: null,       // Post-success hook
            ...options
        };
    }

    async submit() {
        try {
            // 1. Prepare the form data
            const formData = this.collectFormData();
            
            // 2. Apply transformations if needed
            const finalData = this.options.transformData 
                ? await this.options.transformData(formData)
                : formData;

            // 3. Optional pre-submit validation/hook
            if (this.options.beforeSubmit) {
                const shouldProceed = await this.options.beforeSubmit(finalData);
                if (shouldProceed === false) return;
            }

            // 4. Send the request
            const response = await fetch(this.loader.API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(finalData)
            });

            if (!response.ok) {
                const error = await this.parseError(response);
                throw error;
            }

            // 5. Handle success
            const result = await response.json();
            this.handleSuccess(result);

            // 6. Optional post-success hook
            if (this.options.afterSuccess) {
                this.options.afterSuccess(result);
            }

            return result;

        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    collectFormData() {
        const formData = {};
        const form = document.getElementById(this.options.formId);

        if (!form) {
            throw new Error(`Form with ID "${this.options.formId}" not found`);
        }

        // Get all form elements
        const elements = form.elements;

        // Process each form element
        for (let element of elements) {
            if (element.name && element.type !== 'submit') {
                const fieldName = this.options.fieldMappings[element.name] || element.name;
                formData[fieldName] = this.getElementValue(element);
            }
        }

        return formData;
    }

    getElementValue(element) {
        switch (element.type) {
            case 'number':
                return element.valueAsNumber;
            case 'checkbox':
                return element.checked;
            case 'date':
                return element.valueAsDate;
            case 'time':
                return element.valueAsDate;
            default:
                return element.value;
        }
    }

    async parseError(response) {
        try {
            const errorData = await response.json();
            return new Error(errorData.detail || errorData.message || JSON.stringify(errorData));
        } catch {
            return new Error(await response.text());
        }
    }

    handleSuccess(result) {
        const form = document.getElementById(this.options.formId);
        if (form) form.reset();
        
        this.renderer.loadAndRenderItems();
        
        alert(`${this.loader.itemType.charAt(0).toUpperCase() + this.loader.itemType.slice(1)} created successfully! ID: ${result.id}`);
    }

    handleError(error) {
        console.error(`Error creating ${this.loader.itemType}:`, error);
        alert(`Error: ${error.message}`);
    }

    initialize() {
        const form = document.getElementById(this.options.formId);
        if (form) {
            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                await this.submit();
            });
        }
        return this;
    }
}