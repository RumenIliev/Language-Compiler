"""
1.
Read A;
B := A*2;
Write B;

1.
mov eax, A
call input
mov B, A * 2
mov eax, B
call output

2.
Read A;
Read B;
Write A+B;

2.
mov eax, A
call input
mov eax, B
call input
mov eax, A + B
call output

3.
Read A;
Read B;
C := (A*A+B*B)*2;
Write C;

3.
mov eax, A
call input
mov eax, B
call input
mov C, ( A * A + B * B ) * 2)
mov eax, C
call output

"""
