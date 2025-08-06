// Assisted by WCA@IBM
// Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
const url = 'http://localhost:8080/users';

const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const data = {
    user: {
      username: username,
      email: email,
      password: password
    }
  };

  axios.post(url, data)
    .then(response => {
      console.log(response);
      document.getElementById('apiResponse').innerHTML = `Welcome ${response.data.user.username}!`;
    })
    .catch(error => {
      console.error("error: " + error);
      document.getElementById('apiResponse').innerHTML = `Error ${error}!`;
    });
});
