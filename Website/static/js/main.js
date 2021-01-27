//prepoader of the page
window.onload = function () {
  document.body.classList.add('loaded_hiding');
  window.setTimeout(function () {
    document.body.classList.add('loaded');
    document.body.classList.remove('loaded_hiding');
  }, 500);
}

// Custum validation with Bootstrap
var forms = document.querySelectorAll('.needs-validation')
Array.prototype.slice.call(forms)
  .forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
    }, false)
  })

// Switch theme
let switchTheme = document.getElementById('switchTheme')
build_path = (...args) => {
  return args.map((part, i) => {
    if (i === 0) {
      return part.trim().replace(/[\/]*$/g, '')
    } else {
      return part.trim().replace(/(^[\/]*|[\/]*$)/g, '')
    }
  }).filter(x=>x.length).join('/')
}

switchTheme.onclick = function () {
  let theme = document.getElementById('theme')
  let lightTheme = "/static/css/main.css"

  if (theme.getAttribute('href') == lightTheme ) {
    theme.href = "/static/css/main-dark.css";
  } else {
    theme.href = lightTheme;
  }
}
