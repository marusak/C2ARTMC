# pointer variables are : x=1, y=2
# next pointers are : next=0, prev=1
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1),
        ("x=null","00000001",2,2),
        ("new","00000010",1,3),
        ("x.next=null","00000011",1,0,4),
        ("x.next=null","00000100",1,1,5),
        ("if*","00000101",6,12),
        ("new","00000110",2,7),
        ("x.next=y","00000111",2,1,0,8,3),
        ("x.next=y","00001000",1,2,1,9,4),
        ("x.next=null","00001001",2,1,10),
        ("x=y","00001010",1,2,11),
        ("goto","00001011",5),
        ("ifx==null","00001100",1,16,13),
        ("x=y.next","00001101",2,1,0,14),
        ("x=y","00001110",1,2,15),
        ("goto","00001111",12),
        ("goto","00010000",17),
        ("exit","00010001")]
    node_width=18
    pointer_num=3
    desc_num=5
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)