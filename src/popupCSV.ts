document.addEventListener('DOMContentLoaded', () => {
    const csvUploadLabel = document.getElementById('s1UploadFileLabel') as HTMLLabelElement;
    const s1UploadFileInput = document.getElementById('s1UploadFileInput') as HTMLInputElement;
    const step1 = document.getElementById('step1') as HTMLDivElement;
    const step2 = document.getElementById('step2') as HTMLDivElement;
    const step3 = document.getElementById('step3') as HTMLDivElement;
    const s2UsernameColumnSelect = document.getElementById('s2UsernameColumnSelect') as HTMLSelectElement;
    const s2NextBTN = document.getElementById('s2NextBTN') as HTMLButtonElement;
    const s3UsernamesList = document.getElementById('s3UsernamesList') as HTMLDivElement;
    const s3StartBTN = document.getElementById('s3StartBTN') as HTMLButtonElement;

    
    let csvData: string[][] = [];
    let selectedUsernameColumn = 1;

    // Step 1: File upload
    s1UploadFileInput.addEventListener('change', (e) => {
        const file = s1UploadFileInput.files?.[0];
        if (file) {
            csvUploadLabel.textContent = file.name;
            const reader = new FileReader();
            reader.onload = (event) => {
                const result = event.target?.result as string;
                csvData = parseCSV(result);
                moveToStep2();
            };
            reader.readAsText(file);
        } else {
            csvUploadLabel.textContent = "Upload";
        }
    });

    // Step 2: Ask for the username column
    s2NextBTN.addEventListener('click', () => {
        const selectedOption = s2UsernameColumnSelect.options[s2UsernameColumnSelect.selectedIndex];
        if (selectedOption) {
            selectedUsernameColumn = parseInt(selectedOption.value, 10);
            moveToStep3();
        } else {
            alert('Please select a valid username column.');
        }
    });

    function populateColumnDropdown() {
        s2UsernameColumnSelect.innerHTML = '';

        if (csvData.length > 0) {
            const headerRow = csvData[0];
            for (let index = 0; index < headerRow.length; index++) {
                const columnName = headerRow[index];
                if (columnName.trim() !== '') {
                    const option = document.createElement('option');
                    option.text = `Column ${index + 1}: ${columnName}`;
                    option.value = `${index + 1}`;
                    s2UsernameColumnSelect.appendChild(option);
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
            s3UsernamesList.innerHTML = ''

            usernames.forEach((username) => {
                const usernameElement = document.createElement('div');
                usernameElement.textContent = username;
                s3UsernamesList.appendChild(usernameElement);
            });

        } else {
            alert('Please select a valid username column.');
        }
    }

    // Step 4: Manage Access
    s3StartBTN.addEventListener('click', () => {
        alert('Starting management. Please do not close extension');
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
