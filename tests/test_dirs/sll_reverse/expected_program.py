# pointer variables are : t=3, x=1, y=2
# next pointers are : next=0
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",3,1,"NOABSTR"),
        ("ifx==null","00000001",1,7,2),
        ("x=y","00000010",2,1,3,"NOABSTR"),
        ("x=y.next","00000011",1,1,0,4,"NOABSTR"),
        ("x.next=y","00000100",2,3,0,5,4,"NOABSTR"),
        ("x=y","00000101",3,2,6,"NOABSTR"),
        ("goto","00000110",1,"NOABSTR"),
        ("goto","00000111",8,"NOABSTR"),
        ("exit","00001000","NOABSTR")]
    node_width=19
    pointer_num=4
    desc_num=5
    next_num=1
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)