(function(){
  const form=document.getElementById("supportForm"),state=document.getElementById("supportState");
  if(!form)return;
  let busy=false;
  if(BtePortal.getToken())BtePortal.get("/api/v1/auth/me").then(user=>{form.elements.full_name.value=user.display_name||"";form.elements.phone.value=user.phone||"";}).catch(()=>{});
  form.onsubmit=async event=>{
    event.preventDefault();if(busy||!form.reportValidity())return;
    busy=true;const button=form.querySelector("button");button.disabled=true;
    try{const payload={};["full_name","phone","subject","message"].forEach(key=>payload[key]=form.elements[key].value.trim());const result=await BtePortal.post("/api/v1/contacts",payload);state.textContent=result.message+" Mã liên hệ: "+result.id;form.elements.message.value="";}
    catch(error){state.textContent=error.message;}
    finally{busy=false;button.disabled=false;}
  };
})();
