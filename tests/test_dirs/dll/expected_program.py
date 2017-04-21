# pointer variables are : x=1, y=2
# next pointers are : next=0, prev=1
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1,"NOABSTR"),
        ("x=null","00000001",2,2,"NOABSTR"),
        ("new","00000010",1,3,"NOABSTR"),
        ("x.next=null","00000011",1,0,4,"NOABSTR"),
        ("x.next=null","00000100",1,1,5,"NOABSTR"),
        ("if*","00000101",6,12),
        ("new","00000110",2,7,"NOABSTR"),
        ("x.next=y","00000111",2,1,0,8,3,"NOABSTR"),
        ("x.next=y","00001000",1,2,1,9,4,"NOABSTR"),
        ("x.next=null","00001001",2,1,10,"NOABSTR"),
        ("x=y","00001010",1,2,11,"NOABSTR"),
        ("goto","00001011",5,"NOABSTR"),
        ("ifx==null","00001100",1,16,13),
        ("x=y.next","00001101",2,1,0,14,"NOABSTR"),
        ("x=y","00001110",1,2,15,"NOABSTR"),
        ("goto","00001111",12,"NOABSTR"),
        ("goto","00010000",17,"NOABSTR"),
        ("exit","00010001","NOABSTR")]
    node_width=18
    pointer_num=3
    desc_num=5
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)