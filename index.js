// const form = document.querySelector("form")
const form = document.getElementById("addForm");


document.querySelector(".add-button").addEventListener("click", ()=>
    {
    if (form.style.display === 'none') {
      form.style.display = 'flex';
    } else {
      form.style.display = 'none';
    }


})

const tbody = document.querySelector("tbody")
const data = fetch("http://127.0.0.1:5000/api/products").then(res => res.json())
.then(items=>{
  let from = ""
  items.forEach(element => {
    from += `<tr data-id="${element.id}">
    <td>${element.id}</td>
    <td><input type="text" class="name" value="${element.name}"></td>
    <td><input type="text" class="description" value="${element.description}"></td>
    <td><input type="file" class="new-image" accept="image/*"></td>
    <td><img src="${element.image_data}" width="125"></td>
    <td><button class="save-btn">submit</button>
    <button class="delete-btn">delete</button</td>
        </tr>`
  });
  tbody.innerHTML+=from
})
    

const addForm = document.getElementById("addForm");

addForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(addForm);

    const response = await fetch("http://127.0.0.1:5000/insert", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    alert(result.message);

    // reload table after adding
    location.reload();
});


// tbody.addEventListener("click", async function(e) {
//     if (!e.target.classList.contains("save-btn")) return;

//     const row = e.target.closest("tr");
//     const id = row.getAttribute("data-id");

//     const name = row.querySelector(".name").value;
//     const description = row.querySelector(".description").value;
//     const imageFile = row.querySelector(".new-image").files[0];

//     const formData = new FormData();
//     formData.append("name", name);
//     formData.append("description", description);

//     if (imageFile) {
//         formData.append("image", imageFile);
//     }

//     const res = await fetch(`http://127.0.0.1:5000/update/${id}`, {
//         method: "POST",
//         body: formData
//     });

//     const data = await res.json();
//     alert(data.message);
//     location.reload();  
// });

tbody.addEventListener("click", async function(e) {

    // UPDATE BUTTON
    if (e.target.classList.contains("save-btn")) {
        const row = e.target.closest("tr");
        const id = row.getAttribute("data-id");

        const name = row.querySelector(".name").value;
        const description = row.querySelector(".description").value;
        const imageFile = row.querySelector(".new-image").files[0];

        const formData = new FormData();
        formData.append("name", name);
        formData.append("description", description);

        if (imageFile) {
            formData.append("image", imageFile);
        }

        const res = await fetch(`http://127.0.0.1:5000/update/${id}`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        alert(data.message);
        location.reload();
    }

    // DELETE BUTTON
    if (e.target.classList.contains("delete-btn")) {
        const row = e.target.closest("tr");
        const id = row.getAttribute("data-id");

        const res = await fetch(`http://127.0.0.1:5000/delete/${id}`);
        const data = await res.json();

        alert(data.message);
        row.remove();
    }
});
