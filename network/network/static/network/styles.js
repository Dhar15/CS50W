function like(id) {
  var like_btn = document.querySelector(`#like-btn-${id}`);

    if (like_btn.getAttribute('class') == 'fa fa-heart-o') {

    fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: true
        })
    });

    like_btn.setAttribute('class', 'fa fa-heart');
    
    fetch(`/like/${id}`)
    .then((res) => res.json())
    .then((post) => {
        console.log("Before",post);
        post.is_liked = true
        document.querySelector(`#like-count-${id}`).textContent = post.likes;
        window.location.reload();
        console.log("After",post)
    });
    
    }
    else {

    fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: false
        })
        });
        
        like_btn.setAttribute('class', 'fa fa-heart-o');

        fetch(`/like/${id}`)
        .then((res) => res.json())
        .then((post) => {
        console.log("Before",post);
        post.is_liked = false
        document.querySelector(`#like-count-${id}`).textContent = post.likes;
        window.location.reload();
        console.log("After",post);
        });
    }
    return false;
}


function edit(id) {
    var edit_box = document.querySelector(`#edit-box-${id}`);
    var edit_btn = document.querySelector(`#edit-btn-${id}`);
    edit_box.style.display = 'block';
    edit_btn.style.display = 'block'; 
    edit_box.value = document.querySelector(`#post-${id}`).innerHTML;
    document.querySelector(`#post-${id}`).innerHTML = "";

    edit_btn.addEventListener('click', () => {
        fetch('/edit/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                post: edit_box.value
            })
          });
        
          edit_box.style.display = 'none';
          edit_btn.style.display = 'none';

          document.querySelector(`#post-${id}`).innerHTML = edit_box.value;
    });

}
