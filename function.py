def is_even(num):
   return num % 2 == 0

print(is_even(3))
print(is_even(4))

# 计算长方形面积
def calculate_area(length, width):
    return length * width
print(calculate_area(3, 4))

# 你好
def greet(name):
    print(f'你好, {name}!')
greet('vuy')
# 乘积
def multiply(num1, num2):
    return num1 * num2
print(multiply(3, 4))
# 返回列表的最大值
def get_max(lst):
    return max(lst)
print(get_max([1, 2, 3, 4, 5]))
# 检查年龄
def check_age(age):
    if age >= 18:
        return '成年'
    else:
        return '未成年'
print(check_age(18))
# 算总和
def get_sum(*args):
    return sum(args)
print(get_sum(1, 2, 3, 4, 5))