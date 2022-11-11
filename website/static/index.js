function displayModal(element){
  if (element.style.display == 'block' || element.style.display == null)
    {
      element.style.display='none';
    } else {
      element.style.display='block';
    }
}

function bookMark(bookId){
    console.log(bookId)
    fetch('/bookmark-book', {
        method: 'POST',
        body: JSON.stringify({ bookId:bookId })
    }).then((_res) => {
        window.location.reload();
    });
}

function bookmarkChapter(bookId, chapterId){
    fetch('/bookmark-chapter', {
        method: 'POST',
        body: JSON.stringify({ bookId: bookId, chapterId:chapterId})
    }).then((_res) =>{
        window.location.reload();
    });
}

function retrieveBook(bookId){
    window.location.href = "simulator?bookId="+bookId;
}

function retrieveChapters(bookId){
    window.location.href = "chapters?bookId="+bookId;
}

function retrieveChapter(chapterId){
    window.location.href = "view-chapter?chapter="+chapterId;
}

function editBook (bookId){
    window.location.href = "edit-book?bookId="+bookId;
}

function deleteChapter(bookId, chapterId){
    fetch('/delete-chapter', {
        method: 'POST',
        body: JSON.stringify({bookId: bookId, chapterId: chapterId})
        }).then((_res) => {
            window.location.href = "simulator?bookId="+bookId;
        });
}

function deleteBook(bookId){
    fetch('/delete-book', {
        method: 'POST',
        body: JSON.stringify({ bookId: bookId})
    }).then((_res) => {
        window.location.href = "book";
    });
}

function editChapter(bookId, chapterId){
    window.location.href = "edit-chapter?&bookId="+bookId+"&chapterId="+chapterId;
}

function alert_user(dastring, dastring2){
 console.log(dastring + "  " + dastring2);
}

function checkEmail(element){
  if (element.value.includes("@") == false || element.value.includes(".com") == false){
      element.style.borderColor="red";
      emailSubtext.classList="subtext";
      emailSubtext.innerHTML="Invalid Email";
    }
  else{
      emailSubtext.classList="hidden-subtext";
      element.style.borderColor="green";
      }
}

function checkPassword(password, password1){
    if(password == password1){
      document.getElementById('password').style.borderColor='green';
    }
    else
    {
        document.getElementById('')
    }
  }

function generateGenres(book_genre){
    for (x in book_genre){
    print("hello")
    }
}

function addBookhistory(bookId){
    fetch(`/bookhistory/${bookId}`);
}

function addLastchapter(bookId, chapterId) {
    fetch(`/bookhistory/${bookId}/${chapterId}`);
}


//Share button functionality - Steven Chen
function shareButton(){
    // grabs link from current website window
    var link = window.location.href;
    // copies link to clipboard
    navigator.clipboard.writeText(link);
}

// Activate Tooltip for buttons - Steven Chen
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })
  document.getElementById("registerForm").addEventListener("submit",(e)=>{
    e.preventDefault();
    let username = $("#username").val();
    let password = $("#password1").val();
    let passwordConfirm = $("#password2").val();
    let email = $("#email").val()
    if(username.length < 3){
        $("#modalContent").text("Name must me greater than 3 characters");
        $("#modal").modal("show");
        return ;
    }
    if(email.length < 7){
        $("#modalContent").text("The email must be greater than 7 characters");
        $("#modal").modal("show");
        return ;
    }
    if(password.length < 8){
        $("#modalContent").text("The password must be greater than 8 characters");
        $("#modal").modal("show");
        return ;
    }
    if(password != passwordConfirm){
        $("#modalContent").text("passwords do not match");
        $("#modal").modal("show");
        return ;
    }
    e.target.submit();
})