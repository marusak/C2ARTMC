# pointer variables are : element=1, t=4, tmp=2, tmp2=3
# next pointers are : next=0, prev=1
# data values are : 1="00000001"
def get_program():
    program=[
        ("x=y","00000000",2,4,1,"NOABSTR"),
        ("new","00000001",1,2,"NOABSTR"),
        ("ifx==null","00000010",1,3,5,"NOABSTR"),
        ("goto","00000011",19,"NOABSTR"),
        ("goto","00000100",5,"NOABSTR"),
        ("setdata","00000101",1,"00000001",6,"NOABSTR"),
        ("x.next=null","00000110",1,0,7,"NOABSTR"),
        ("ifx==null","00000111",4,8,11,"NOABSTR"),
        ("x.next=null","00001000",1,1,9,"NOABSTR"),
        ("goto","00001001",19,"NOABSTR"),
        ("goto","00001010",11,"NOABSTR"),
        ("x=y.next","00001011",3,2,0,12,"NOABSTR"),
        ("ifx==null","00001100",3,16,13),
        ("x=y.next","00001101",2,2,0,14,"NOABSTR"),
        ("x=y.next","00001110",3,2,0,15,"NOABSTR"),
        ("goto","00001111",12,"NOABSTR"),
        ("x.next=y","00010000",2,1,0,17,4,"NOABSTR"),
        ("x.next=y","00010001",1,2,1,18,5,"NOABSTR"),
        ("goto","00010010",19,"NOABSTR"),
        ("exit","00010011","NOABSTR")]
    node_width=21
    pointer_num=5
    desc_num=6
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)