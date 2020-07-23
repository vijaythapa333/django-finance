const searchField = document.querySelector('#searchField');

const appTable = document.querySelector('.app-table')

const paginationContainer = document.querySelector('.pagination-container')

const tableOutput = document.querySelector('.table-output');
tableOutput.style.display = 'none';

const tbody = document.querySelector('.table-body')


searchField.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value;

    // Check whether the user has typed anything on search box or not
    if(searchValue.trim().length>0){
        // If typed, hide main table and display search-based table
        console.log('searchValue', searchValue);
        paginationContainer.style.display = 'none'

        tbody.innerHTML = "";

        // Making an API call
        fetch('/search-expenses/', {
            body: JSON.stringify({searchText: searchValue}), 
            method: 'POST',
        })
        .then(res=>res.json())
        .then(data=>{
            console.log('data', data)
            
            appTable.style.display = 'none'
            tableOutput.style.display = 'block';

            if(data.length===0){
                tableOutput.innerHTML = '<div class="alert alert-secondary" role="alert">No results found.</div>'
            }
            else
            {
                data.forEach(item => {
                    tbody.innerHTML += `
                    <tr>
                        <td>${item.description}</td>
                        <td>${item.category_id}</td>
                        <td>${item.amount}</td>
                        <td>${item.date}</td>
                    </tr>
                    
                    `
                });
                
            }
        });
    }
    else
    {
        // if not typed, display main table
        appTable.style.display = 'block';
        paginationContainer.style.display = 'block';
        tableOutput.style.display = 'none';
    }
});