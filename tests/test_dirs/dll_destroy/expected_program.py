# pointer variables are : next=7, pn=2, pt=1, v0=3, v1=5, v2=6, v3=8
# next pointers are : l=0, r=1
# data values are : 
def get_program():
    program=[
        ("new","00000000",1,1),
        ("x.next=null","00000001",1,0,2),
        ("x.next=null","00000010",1,1,3),
        ("if*","00000011",4,17),
        ("x=y","00000100",2,1,5),
        ("if*","00000101",6,10),
        ("ifx==null","00000110",2,9,7),
        ("x=y.next","00000111",2,2,0,8),
        ("goto","00001000",6),
        ("goto","00001001",13),
        ("ifx==null","00001010",2,13,11),
        ("x=y.next","00001011",2,2,1,12),
        ("goto","00001100",10),
        ("new","00001101",2,14),
        ("x.next=null","00001110",2,0,15),
        ("x.next=null","00001111",2,1,16),
        ("goto","00010000",3),
        ("x=y.next","00010001",3,1,0,18),
        ("ifx==null","00010010",3,23,19),
        ("x=y.next","00010011",5,1,0,20),
        ("x=y.next","00010100",4,5,0,21),
        ("x.next=y","00010101",1,4,0,22,3),
        ("goto","00010110",17),
        ("x=y.next","00010111",6,1,1,24),
        ("ifx==null","00011000",6,29,25),
        ("x=y.next","00011001",8,1,1,26),
        ("x=y.next","00011010",7,8,1,27),
        ("x.next=y","00011011",1,7,1,28,4),
        ("goto","00011100",23),
        ("goto","00011101",30),
        ("exit","00011110")]
    node_width=23
    pointer_num=8
    desc_num=5
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)