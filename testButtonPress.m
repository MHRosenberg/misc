
while true
   k = waitforbuttonpress;
   f = gcf;
   display(f.CurrentCharacter)
   if f.CurrentCharacter == '[';
      display('yup') 
   end
end