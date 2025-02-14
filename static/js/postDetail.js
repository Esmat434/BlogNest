const btn_like = document.getElementById('btn_like')
const input_like = document.getElementById('input_like')

btn_like.addEventListener('click', ()=>{
    input_like.click()
})

const btn_reply = document.getElementById('reply_btn')
const child_comment_input = document.getElementById('child_comment')
const child_comment_btn = document.getElementById('child_comment_btn')

btn_reply.addEventListener('click',()=>{
    child_comment_input.style.display = child_comment_input.style.display === 'none'?'block':'none'
    child_comment_btn.style.display = child_comment_btn.style.display === 'none'?'block':'none'
})