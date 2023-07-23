function likePost(user_id, post_id){
  fetch("like_post/" + user_id + "/" + post_id)
    .then((response) => {
      document.getElementById("likes_count").innerHTML = response.json();
    }).catch(e => {
      console.log(e); // https://www.codegrepper.com/code-examples/javascript/uncaught+in+promise+error
  });
    location.reload(); // https://www.w3schools.com/jsref/met_loc_reload.asp
  };

function unlikePost(user_id, post_id){
  fetch("unlike_post/" + user_id + "/" + post_id)
    .then((response) => {
      document.getElementById("likes_count").innerHTML = response.json();
    }).catch(e => {
      console.log(e); 
  });
    location.reload();
  };

// function editPost(post_id){
//   var field = document.getElementById("edit_form");
//   field.style.display = "none";
//   if (field.style.display === "none") {
//     field.style.display = "block";
//   } else {
//     field.style.display = "none";
//   }
// }
  

