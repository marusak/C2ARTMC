# pointer variables are : x=1, y=2
# next pointers are : next1=0, next2=1, prev1=2, prev2=3
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1),
        ("x=null","00000001",2,2),
        ("new","00000010",1,3),
        ("x.next=null","00000011",1,0,4),
        ("x.next=null","00000100",1,1,5),
        ("x.next=null","00000101",1,2,6),
        ("x.next=null","00000110",1,3,7),
        ("if*","00000111",8,17),
        ("new","00001000",2,9),
        ("x.next=y","00001001",2,1,0,10,3),
        ("x.next=y","00001010",2,1,1,11,4),
        ("x.next=y","00001011",1,2,2,12,5),
        ("x.next=y","00001100",1,2,3,13,6),
        ("x.next=null","00001101",2,2,14),
        ("x.next=null","00001110",2,3,15),
        ("x=y","00001111",1,2,16),
        ("goto","00010000",7),
        ("ifx==null","00010001",1,21,18),
        ("x=y.next","00010010",2,1,0,19),
        ("x=y","00010011",1,2,20),
        ("goto","00010100",17),
        ("goto","00010101",22),
        ("exit","00010110")]
    node_width=20
    pointer_num=3
    desc_num=7
    next_num=4
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)