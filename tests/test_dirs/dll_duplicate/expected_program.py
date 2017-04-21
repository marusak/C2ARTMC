# pointer variables are : x=1, y=2
# next pointers are : next1=0, next2=1, prev1=2, prev2=3
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1,"NOABSTR"),
        ("x=null","00000001",2,2,"NOABSTR"),
        ("new","00000010",1,3,"NOABSTR"),
        ("x.next=null","00000011",1,0,4,"NOABSTR"),
        ("x.next=null","00000100",1,1,5,"NOABSTR"),
        ("x.next=null","00000101",1,2,6,"NOABSTR"),
        ("x.next=null","00000110",1,3,7,"NOABSTR"),
        ("if*","00000111",8,17),
        ("new","00001000",2,9,"NOABSTR"),
        ("x.next=y","00001001",2,1,0,10,3,"NOABSTR"),
        ("x.next=y","00001010",2,1,1,11,4,"NOABSTR"),
        ("x.next=y","00001011",1,2,2,12,5,"NOABSTR"),
        ("x.next=y","00001100",1,2,3,13,6,"NOABSTR"),
        ("x.next=null","00001101",2,2,14,"NOABSTR"),
        ("x.next=null","00001110",2,3,15,"NOABSTR"),
        ("x=y","00001111",1,2,16,"NOABSTR"),
        ("goto","00010000",7,"NOABSTR"),
        ("ifx==null","00010001",1,21,18),
        ("x=y.next","00010010",2,1,0,19,"NOABSTR"),
        ("x=y","00010011",1,2,20,"NOABSTR"),
        ("goto","00010100",17,"NOABSTR"),
        ("goto","00010101",22,"NOABSTR"),
        ("exit","00010110","NOABSTR")]
    node_width=20
    pointer_num=3
    desc_num=7
    next_num=4
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)