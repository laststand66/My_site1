//сайдбар

$(document).ready(function() {
  $(".select-link a:nth-child(1)").click(function() {
    $(".side-bar-content ul").hide();
    $(".side-bar-content ul:nth-child(1)").show();
  });

  $(".select-link a:nth-child(2)").click(function() {
    $(".side-bar-content ul").hide();
    $(".side-bar-content ul:nth-child(2)").show();
  });

  $(".select-link a:nth-child(3)").click(function() {
    $(".side-bar-content ul").hide();
    $(".side-bar-content ul:nth-child(3)").show();
  });

  //селект

  /*  //как сделать ,чтобы рабоатло?
  function click_show() {
    $(".icon-select").click(function() {
      $(".box-for-select option").show();
    });
  }
  function click_hide() {
    $(".icon-select").click(function click_hide() {
      $(".box-for-select option").hide();
    });
  }

  $(".icon-select").click("click", click_show());
  $(".icon-select").addEventListener("click", click_hide());
  */

  $(".name-select").click(function() {
    $(".box-for-select option").toggle();
  });
  $(".box-for-select option").click(function() {
    $(".box-for-select option").hide();
  });
});

//select

/*
  
  $(".icon-select").click(function click_show() {
    ($("box-for-select option").attr("display") == "none")
    $(".box-for-select option").show();

    $(".box-for-select option").hide();
  });

  $(".icon-select").click(function click_hide() {
    $(".box-for-select option").hide();
  });

  if ($("box-for-select option").attr("display") == "none") {
    click_show;
  } else {
    click_hide;
  }


while ($("box-for-select option").attr("display") == "none")
*/
