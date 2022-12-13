const image_input = document.querySelector("#image-input");
image_input.addEventListener("change", function() {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image").style.backgroundImage = `url(${uploaded_image})`;
});
reader.readAsDataURL(this.files[0]);
});



$(document).ready(function() {

    
    var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            }
    
            reader.readAsDataURL(input.files[0]);
        }
    }
    

    $(".file-upload").on('change', function(){
        readURL(this);
    });
    
    $(".upload-button").on('click', function() {
        $(".file-upload").click();
    });
});



function myFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("mySearch");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myMenu");
    li = ul.getElementsByTagName("li");

  // Loop through all list items, and hide those who don't match the search query
for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
    } else {
        li[i].style.display = "none";
    }
}
}
