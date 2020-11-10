
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email when form is submitted
  document.querySelector('#compose-form').onsubmit = submitForm;

  // By default, load the inbox
  load_mailbox('inbox');
});

function submitForm() {

  //Get values from the form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  send_email(recipients, subject, body);
  return false;
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(recipients, subject, body) {

  // Post the emails
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject:  subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(email => {
    console.log(email);
    load_mailbox('sent');
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  var email_view = document.querySelector('#emails-view')

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the emails 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    if (emails.length == 0) {
      const item = document.createElement('p');
      item.setAttribute('class', 'no-mail');
      item.innerHTML = 'No emails yet!';


      document.querySelector('#emails-view').append(item);
    }
    emails.forEach(email => add_email(email));
  });
}

function add_email(email) {
  const item = document.createElement('div');
  item.setAttribute('id', email.id);
  item.setAttribute('class', 'container mail-item');

  const row = document.createElement('div');
  row.setAttribute('id', `${email.id}-row`);
  row.setAttribute('class', 'row');
  
  //White background for unread email, gray otherwise
  row.style.backgroundColor = email.read ? '#D3D3D3' : '#FFFFFF';

  const sender = document.createElement('div');
  sender.setAttribute('class', 'col sender');
  sender.innerHTML = email.sender;

  const subject = document.createElement('div');
  subject.setAttribute('class', 'col-6 subject');
  subject.innerHTML = email.subject;

  const timestamp = document.createElement('div');
  timestamp.setAttribute('class', 'col timestamp');
  timestamp.innerHTML = email.timestamp;

  item.addEventListener('click', () => view_email(email.id));

  // Add the content to our page
  document.querySelector('#emails-view').append(item);
  document.getElementById(email.id).appendChild(row);
  document.getElementById(`${email.id}-row`).appendChild(sender);
  document.getElementById(`${email.id}-row`).appendChild(subject);
  document.getElementById(`${email.id}-row`).appendChild(timestamp);
}

function view_email(email_id) {

  // Get email of a particular id
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    render_email(email);
    if(!email.read) {
      mark_read(email_id);
    }
  });
}

function render_email(email) {
   // Show the mailbox and hide other views
   document.querySelector('#emails-view').style.display = 'none';
   document.querySelector('#compose-view').style.display = 'none';
   document.querySelector('#email-view').style.display = 'block';

   document.getElementById('email-from').innerHTML = email.sender; 
   document.getElementById('email-to').innerHTML = email.recipients; 
   document.getElementById('email-subject').innerHTML = email.subject; 
   document.getElementById('email-timestamp').innerHTML = email.timestamp; 
   document.getElementById('email-body').innerHTML = email.body + "\n";  

   document.getElementById('reply').removeEventListener('click', reply);
   document.getElementById('reply').addEventListener('click', () => reply(email));

   // Archive button
   archive(email.id);
}

function reply(email) {
  compose_email();

  const subject = `${email.subject.substring(0, 4) === 'Re: ' ? '' : 'Re: '}${email.subject}`;
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body} \n`;
}

// Mark email as read
function mark_read(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',  
    body: JSON.stringify({
      read: true
    })
  });
}

function archive(email_id) {
  document.getElementById('archive-button').innerHTML = '';

  const mailbox = document.querySelector('h3').innerHTML;
  const color = (mailbox == 'Inbox') ? 'danger' : 'primary';

  if(mailbox != 'Sent') {
    const archive_button = document.createElement('button');
    archive_button.setAttribute('id', 'archive');
    archive_button.setAttribute('class', `btn btn-sm btn-${color}`);
    archive_button.innerHTML = (mailbox == 'Inbox') ? 'Archive' : 'Unarchive';
    archive_button.addEventListener('click', () => toggle_archive(email_id, mailbox));

    document.getElementById('archive-button').append(archive_button);
  }
}

function toggle_archive(email_id, mailbox) {
  const status = mailbox == 'Inbox' ? false : true;

  // Mark email as archived/unarchived
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !status
    })
  })
  .then(() => load_mailbox('inbox'));
}
