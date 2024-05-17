
function openModal() {
    document.getElementById('addBlogModal').classList.remove('hidden');
    document.getElementById('addblogbutton').classList.add('hidden');
}

function closeModal() {
    document.getElementById('addBlogModal').classList.add('hidden');
    document.getElementById('addblogbutton').classList.remove('hidden');
}

window.onclick = function (event) {
    let modal = document.getElementById('addBlogModal');
    if (event.target === modal) {
        closeModal();
    }
}


function openModalProfile(id) {
    document.getElementById(id).classList.remove('hidden');
}

function closeModalProfile(id) {
    document.getElementById(id).classList.add('hidden');
}


function messageclose() {
    var messageDiv = document.getElementById('flash-message');
    messageDiv.style.opacity = '0'; 
    setTimeout(function() {
        messageDiv.style.display = 'none'; 
    }, 600); 
}

setTimeout(messageclose, 3000);


