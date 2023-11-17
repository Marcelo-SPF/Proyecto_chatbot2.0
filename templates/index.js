var message = [
    "Hola, soy el tio y tu?",
    "Encantado de conocerlo",
    "Como estas?",
    "No esta mal, gracias",
    "A que te dedicas?",
    "Eso es genial",
    "O es un buen lugar para quedarse",
    "Creo que eres una buena persona",
    "Por que piensas eso?",
    "Puedes explicar?",
    "De todos modos tengo que irme ahora",
    "Fue un placer charlar contigo",
    "Es hora de crear un nuevo codepen",
    "Adios",
    ":)"
  ];
  
  $(document).ready(function () {
    setTimeout(function () {
      loader();
      setTimeout(function () {
        $(".container- .display .lds-ellipsis").fadeOut(0);
        reply();
      }, 1600);
    }, 1000);
  });
  
  var scrollctr = 200;
  var i = 0;
  
  function scrollUpdate() {
    lastElementTop = $(".display").position().top;
    scrollAmount = lastElementTop + scrollctr;
    scrollctr += 200;
    $(".display").animate({ scrollTop: scrollAmount }, 700);
  }
  
  function msngr() {
    var msg = $(".text input").val();
    $(".container- .display").append("<div class='msg'><p>" + msg + "</p></div>");
    $(".text input").val("");
  }
  function reply() {
    if (i >= 15) {
      i = 15;
    }
    $(".container- .display").append(
      "<div class='reply'><p>" + message[i] + "</p></div>"
    );
    i++;
  }
  function loader() {
    $(".container- .display").append(
      "<div class='lds-ellipsis'><div></div><div></div><div></div><div></div></div>"
    );
  }
  
  $(".tray .fa-paper-plane").click(msngr);
  $(document).on("keypress", function (e) {
    if (e.which == 13) {
      e.preventDefault();
      msngr();
      scrollUpdate();
    }
  });
  
  $(".tray .fa-paper-plane").click(function () {
    setTimeout(function () {
      scrollUpdate();
      loader();
      setTimeout(function () {
        $(".container- .display .lds-ellipsis").fadeOut(0);
        reply();
        scrollUpdate();
      }, 1600);
    }, 1000);
  });
  $(document).on("keypress", function (e) {
    if (e.which == 13) {
      e.preventDefault();
      setTimeout(function () {
        scrollUpdate();
        loader();
        setTimeout(function () {
          $(".container- .display .lds-ellipsis").fadeOut(0);
          reply();
          scrollUpdate();
        }, 1600);
      }, 1000);
    }
  });
  