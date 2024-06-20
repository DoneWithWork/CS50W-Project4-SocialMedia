
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
async function like(event) {
    event.preventDefault();
    const form = event.target;
    const post_id = form.post_id.value;
    const likesElement = form.querySelector(`div p`);

   console.log(likesElement)
  
    const responce = await fetch(`/like/${post_id}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    if(responce.ok){
        const data = await responce.json();
        const likes = data.likes;
        likesElement.innerText = likes;
        form.querySelector('input[type="submit"]').value = data.liked ? 'Unlike' : 'Like';
        console.log(likes)
    }

}


async function EditPost(event){
    event.preventDefault();
    console.log("edit")
    const form = event.target;
    const content = form.content.value;
    const post_id = form.post_id.value;
    console.log(content)
    const responce = await fetch(`/edit/${post_id}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
             'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: content
        })
    })
    console.log("res")
    console.log(responce)
    if(responce.ok){
        const data = await responce.json();
        console.log(data)
        const content = data.content;
        const textarea = document.querySelector(`#edit-content-${post_id}`);
        const contentElement = document.querySelector(`#content-${post_id}`);
        contentElement.style.display = 'block';
        textarea.style.display = 'none';
        contentElement.innerText = content;
    
    }
}
function edit(event){
    const btn = event.target;
    const postId = btn.getAttribute('data-postId');
    const textarea = document.querySelector(`#edit-content-${postId}`);
    const content = document.querySelector(`#content-${postId}`);
    content.style.display = 'none';
    textarea.style.display = 'block';
   
  
}
function cancel(event){

}