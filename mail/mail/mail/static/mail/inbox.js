document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    
   
    // element.id

   // By default, load the inbox
   load_mailbox('inbox');
   });

 function archive(id) {
    
     fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                 
                 archived: true
                 
             })

     })
     .catch(error => {
             console.log('Error:' ,error )
         })
     setTimeout(() => {load_mailbox('inbox'); }, 500 ) ;
 }

 function unarchive(id) {
    
    fetch(`/emails/${id}`, {
           method: 'PUT',
           body: JSON.stringify({
                
                archived: false
                
             })

      })
      .catch(error => {
             console.log('Error:' ,error )
         })
    setTimeout(() => {load_mailbox('inbox'); }, 1500 ) ;
 }

 function email(id) {
     document.querySelector('#emails-view').style.display = 'none';
     document.querySelector('#compose-view').style.display = 'none';
     document.querySelector('#em').style.display = 'none';
     document.querySelector('#mail').style.display = 'block';

     
     fetch(`/emails/${id}`)
     .then(response => response.json())
     .then(email => {
         let s = email.sender;
         let r = email.recipients;
         let ss = email.subject;
         let t = email.timestamp;
         let b = email.body;
         // email.read = true; put method
         if (ss =='') {
             ss = 'No Subject';
         }
         document.querySelector('#mail').innerHTML = `<h2> ${ss} </h2>`;
         let strong = document.createElement('strong');
         strong.innerHTML = 'From: '
         document.querySelector('#mail').append(strong);
         document.querySelector('#mail').append(`${s}`);
         let br = document.createElement('br')
         document.querySelector('#mail').append(br);
         let strongg = document.createElement('strong');
         strongg.innerHTML = 'To: '
         document.querySelector('#mail').append(strongg);
         document.querySelector('#mail').append(`${r}`);
         let hr = document.createElement('hr');
         document.querySelector('#mail').append(hr);
         let small = document.createElement('div')
         small.innerHTML= `<small>${t}</small>`
         small.style.position = 'absolute';
         small.style.right = '10px';
         document.querySelector('#mail').append(small);
         let body = document.createElement('div');
         body.innerHTML = b;
         body.className = 'body';
         body.style.position = 'absolute';
         body.style.top = '160px';
         document.querySelector('#mail').append(body);
         let reply = document.createElement('button');
         reply.innerHTML = 'Reply'; 
         reply.className = "btn btn-primary";
         reply.id= 'r'
         document.querySelector('#mail').append(reply);
         reply.addEventListener('click', ()=> {
             document.querySelector('#emails-view').style.display = 'none';
             document.querySelector('#compose-view').style.display = 'block';
             document.querySelector('#em').style.display = 'none';
             document.querySelector('#mail').style.display = 'none';

             document.querySelector('#compose-recipients').value= s;
             var tr = ss.startsWith('Re: ');
             if (tr) {
                 document.querySelector('#compose-subject').value= ss;
             } else {
                 document.querySelector('#compose-subject').value= `Re: ${ss}`;

             }
             document.querySelector('#compose-body').value = `On ${t}  ${s} wrote: \n\n${b}\n-----------------------------------------------------------------------------------\n`
             document.querySelector('form').onsubmit = function () {
     let r = document.querySelector('#compose-recipients').value;
     let s = document.querySelector('#compose-subject').value;
     let b = document.querySelector('#compose-body').value;
     
     
     
     fetch('/emails', {
       method: 'POST',
       body: JSON.stringify({
            recipients: r,
            subject: s,
            body: b
         })

      })
     .then(response => response.json())
     .then(() => {
        // Print result
        let m = document.createElement('div');
     m.innerHTML = 'Email sent successfully.' ;
     m.className = 'alert alert-primary';
     m.id = 'm'
     load_mailbox('sent');
     document.querySelector('#emails-view').prepend(m);
     m.addEventListener('animationend', () => {
         m.remove();
     })

     })
     .catch(error => {
             console.log('Error:' ,error )
         })

     document.querySelector('#compose-recipients').value = '';
     document.querySelector('#compose-subject').value = '';
     document.querySelector('#compose-body').value = '';
     
     
     

     return false;
             }

         });
       
     })
     fetch(`/emails/${id}`, {
           method: 'PUT',
           body: JSON.stringify({
                
                read: true
                
             })

      })
      .catch(error => {
             console.log('Error:' ,error )
         })
 } 

 function compose_email() {

 // Show compose view and hide other views
 document.querySelector('#emails-view').style.display = 'none';
 document.querySelector('#compose-view').style.display = 'block';
 document.querySelector('#em').style.display = 'none';
 document.querySelector('#mail').style.display = 'none';
 document.querySelector('#compose-recipients').value = '';
     document.querySelector('#compose-subject').value = '';
     document.querySelector('#compose-body').value = '';



 document.querySelector('form').onsubmit = function () {
     let r = document.querySelector('#compose-recipients').value;
     let s = document.querySelector('#compose-subject').value;
     let b = document.querySelector('#compose-body').value;
     
     
     
     fetch('/emails', {
       method: 'POST',
       body: JSON.stringify({
            recipients: r,
            subject: s,
            body: b
         })

      })
     .then(response => response.json())
     .then(() => {
        // Print result
        let m = document.createElement('div');
     m.innerHTML = 'Email sent successfully.' ;
     m.className = 'alert alert-primary';
     m.id = 'm'
     load_mailbox('sent');
     document.querySelector('#emails-view').prepend(m);
     m.addEventListener('animationend', () => {
         m.remove();
     })

     })
     .catch(error => {
             console.log('Error:' ,error )
         })

     document.querySelector('#compose-recipients').value = '';
     document.querySelector('#compose-subject').value = '';
     document.querySelector('#compose-body').value = '';
     
     
     

     return false;
 
}
 }

 function load_mailbox(mailbox) {
     document.querySelector('#em').innerHTML = '';

  fetch(`/emails/${mailbox}`)
 .then(response => response.json())
 .then(emails => {
   // Print emails
   emails.forEach( element => {
       let div  = document.createElement('div');
       div.className= 'div';
       
       
       let but = document.createElement('button');
       but.className='arc';
       but.innerHTML= '<i class="fa fa-archive"></i> Archive';
       but.addEventListener('click', () => archive(element.id))
     
      
       let a = document.createElement('a');
       div.append(but);
       
       a.dataset.id = element.id;
       a.id = `e${element.id}`;
       a.onmouseover="this.style.backgroundColor='red'";
       a.onmouseout = "this.style.backgroundColor='white'";
       if (element.recipients == element.sender){
           element.sender = 'Me';
           element.recipients = 'Me';

            
             if (element.subject === ''){
                 element.subject = 'No subject';

         }
         }
       a.innerHTML = `${element.sender}<strong style="position: absolute; left: 40%;">${element.subject}</strong><small style="position: absolute; right: 10px;"> ${element.timestamp}</small> `;
       if (element.subject === ''){
         a.innerHTML = `${element.sender}<strong style="position: absolute; left: 40%;">No Subject</strong> <small style="position: absolute; right: 10px;"> ${element.timestamp}</small>`
       }
       if (element.read === true) {
           a.style.backgroundColor='#eae9e9'
       }
      
       
       if (mailbox === 'sent'){
         a.innerHTML = `To: ${element.recipients}<strong style="position: absolute; left: 40%;">${element.subject}</strong><small style="position: absolute; right: 10px;"> ${element.timestamp}</small>`;
         
         if (element.subject === ''){
             a.innerHTML = `To: ${element.recipients}<strong style="position: absolute; left: 40%;">No Subject</strong> <small style="position: absolute; right: 10px;"> ${element.timestamp}</small>`;
         
         }
         
       
       }
       a.href = '#';
       a.className = "list-group-item list-group-item-action";
       div.append(a);
       a.style.width='85%';
      
      
       a.addEventListener('mouseover', () => {
          
          a.style.backgroundColor= 'rgb(220, 237, 255)'; 
          
      
       })

       a.addEventListener('mouseout', () => {
          a.style.backgroundColor= 'white';
          
          if (element.read === true) {
           a.style.backgroundColor='#eae9e9'
       }
       })
       
       a.addEventListener('click',() => email(element.id));


     document.querySelector('#em').append(div)
     if (mailbox === 'sent'){
         but.remove();
         a.style.width='100%'
          
      
     }

     if (mailbox === 'archive'){
        
         but.innerHTML= '<i class="fa fa-chain-broken"></i> Unarchive';
         but.addEventListener('click', () => unarchive(element.id))
        
         
      
     }

   });


  // ... do something else with emails ...
 });

 // Show the mailbox and hide other views
 document.querySelector('#emails-view').style.display = 'block';
 document.querySelector('#compose-view').style.display = 'none';
 document.querySelector('#em').style.display = 'block';
 document.querySelector('#mail').style.display = 'none';



 // Show the mailbox name
 document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

 }