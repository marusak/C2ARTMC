# pointer variables are : x=1, y=2
# next pointers are : next=0, prev=1
# data values are : 
def get_program():
    program=[
        ("x=null","00000000",1,1,"NOABSTR"),
        ("x=null","00000001",2,2,"NOABSTR"),
        ("new","00000010",2,3,"NOABSTR"),
        ("x.next=y","00000011",2,1,0,4,3,"NOABSTR"),
        ("x=y","00000100",1,2,5,"NOABSTR"),
        ("new","00000101",2,6,"NOABSTR"),
        ("x.next=y","00000110",2,1,0,7,4,"NOABSTR"),
        ("x.next=y","00000111",1,2,1,8,5,"NOABSTR"),
        ("x=y","00001000",1,2,9,"NOABSTR"),
        ("if*","00001001",10,19),
        ("new","00001010",2,11,"NOABSTR"),
        ("x.next=y","00001011",2,1,0,12,6,"NOABSTR"),
        ("x.next=y","00001100",1,2,1,13,7,"NOABSTR"),
        ("x=y","00001101",1,2,14,"NOABSTR"),
        ("new","00001110",2,15,"NOABSTR"),
        ("x.next=y","00001111",2,1,0,16,8,"NOABSTR"),
        ("x.next=y","00010000",1,2,1,17,9,"NOABSTR"),
        ("x=y","00010001",1,2,18,"NOABSTR"),
        ("goto","00010010",9,"NOABSTR"),
        ("ifx==null","00010011",2,25,20),
        ("x=y","00010100",1,2,21,"NOABSTR"),
        ("x=y.next","00010101",2,2,0,22,"NOABSTR"),
        ("x=y","00010110",1,2,23,"NOABSTR"),
        ("x=y.next","00010111",2,2,0,24,"NOABSTR"),
        ("goto","00011000",19,"NOABSTR"),
        ("goto","00011001",26,"NOABSTR"),
        ("exit","00011010","NOABSTR")]
    node_width=23
    pointer_num=3
    desc_num=10
    next_num=2
    err_line="11111111"
    restrict_var=1

    env=(node_width, pointer_num, desc_num, next_num, err_line,restrict_var)
    return(program, env)