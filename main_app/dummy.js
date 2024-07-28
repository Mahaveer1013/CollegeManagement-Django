const dummyjson = require('dummy-json');

// Custom helper to generate random time
dummyjson.registerHelper('time', function() {
    const hours = String(Math.floor(Math.random() * 24)).padStart(2, '0');
    const minutes = String(Math.floor(Math.random() * 60)).padStart(2, '0');
    const seconds = String(Math.floor(Math.random() * 60)).padStart(2, '0');
    const milliseconds = String(Math.floor(Math.random() * 1000000)).padStart(6, '0');
    return `${hours}:${minutes}:${seconds}.${milliseconds}`;
});

const balz = `
  {
      "model": "main_app.customuser",
      "pk": 2,
      "fields": {
          "email": "{{email}}",
          "user_type": "3",
          "gender": "{{random 'M' 'F'}}",
          "profile_pic": "path/to/profile_pic.jpg",
          "address": "{{int 1 100}} {{street}}",
          "fcm_token": "default_token",
          "created_at": "{{date '2024-06-01' '2025-06-30'}} {{time}}",
          "updated_at": "{{date '2024-06-01' '2025-06-30'}} {{time}}",
          "password": "pbkdf2_sha256$216000$rNF8ddjqvaMi$KrJ+6p368pKlwW38eqK3Z97ZlFmdFleZtdWjCwhyOWo="
      }
  }
`;

const result = dummyjson.parse(balz); // Returns a string
console.log(result);
