function like(blogId) {
    const likeCount = document.getElementById(`likes-count-${blogId}`);
    const likeButton = document.getElementById(`like-button-${blogId}`);
  
    fetch(`/blogs/likeblog/${blogId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
          likeButton.className = "fas fa-thumbs-up";
        } else {
          likeButton.className = "far fa-thumbs-up";
        }
      })
      .catch((e) => alert("An error occured while liking the post. Please try again."));
  }