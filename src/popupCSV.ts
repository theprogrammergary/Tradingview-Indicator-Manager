document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('csvFileInput') as HTMLInputElement;

    fileInput.addEventListener('change', (e) => {
        const uploadedFile = fileInput.files?.[0];

        if (uploadedFile) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const csvContent = event.target?.result as string;
                console.log('CSV content:', csvContent);
            };
            reader.readAsText(uploadedFile);
        } else {
            console.log('No file selected.');
        }
    });
});
