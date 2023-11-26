document.addEventListener('DOMContentLoaded', () => {
    const csvUploadForm = document.getElementById('csvUploadForm') as HTMLFormElement;
    const csvFileInput = document.getElementById('csvFileInput') as HTMLInputElement;
    const step1 = document.getElementById('step1') as HTMLDivElement;
    const step2 = document.getElementById('step2') as HTMLDivElement;
    const step3 = document.getElementById('step3') as HTMLDivElement;
    const usernameColumnSelect = document.getElementById('usernameColumnSelect') as HTMLSelectElement;
    const confirmColumnBtn = document.getElementById('confirmColumnBtn') as HTMLButtonElement;
    const usernamesList = document.getElementById('usernamesList') as HTMLDivElement;
    const startManagementBtn = document.getElementById('startManagementBtn') as HTMLButtonElement;

    
    let csvData: string[][] = [];
    let selectedUsernameColumn = 1;

    // Step 1: File upload
    csvUploadForm.addEventListener('change', (e) => {
        const file = csvFileInput.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const result = event.target?.result as string;
                csvData = parseCSV(result);
                moveToStep2();
            };
            reader.readAsText(file);
        }
    });

    // Step 2: Ask for the username column
    confirmColumnBtn.addEventListener('click', () => {
        const selectedOption = usernameColumnSelect.options[usernameColumnSelect.selectedIndex];
        if (selectedOption) {
            selectedUsernameColumn = parseInt(selectedOption.value, 10);
            moveToStep3();
        } else {
            alert('Please select a valid username column.');
        }
    });

    function populateColumnDropdown() {
        usernameColumnSelect.innerHTML = '';

        if (csvData.length > 0) {
            const headerRow = csvData[0];
            for (let index = 0; index < headerRow.length; index++) {
                const columnName = headerRow[index];
                if (columnName.trim() !== '') {
                    const option = document.createElement('option');
                    option.text = `Column ${index + 1}: ${columnName}`;
                    option.value = `${index + 1}`;
                    usernameColumnSelect.appendChild(option);
                }
            }
        } else {
            alert('No data available. Please upload a valid CSV file first.');
            moveToStep1();
        }
    }


    // Step 3: Show values from the selected column
    function populateUsernameList() {
        if (selectedUsernameColumn > 0) {
            const usernames = csvData.map((row) => row[selectedUsernameColumn - 1]);
            usernames.shift();
            usernamesList.innerHTML = ''

            usernames.forEach((username) => {
                const usernameElement = document.createElement('div');
                usernameElement.textContent = username;
                usernamesList.appendChild(usernameElement);
            });

        } else {
            alert('Please select a valid username column.');
        }
    }

    // Step 4: Manage Access
    startManagementBtn.addEventListener('click', () => {
        alert('Starting management. You can add your code here.');
    });



    function moveToStep1() {
        step2.classList.add('hidden');
        step1.classList.remove('hidden');
    }

    function moveToStep2() {
        step1.classList.add('hidden');
        step2.classList.remove('hidden');
        populateColumnDropdown();
    }

    function moveToStep3() {
        step2.classList.add('hidden');
        step3.classList.remove('hidden');
        populateUsernameList();
    }

    function parseCSV(csvText: string): string[][] {
        const rows = csvText.split('\n');
        const data = rows.map((row) => row.split(','));
        return data;
    }
});
