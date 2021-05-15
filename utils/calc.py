from main.models import RatingCalc

def create_calc(user_id, check_sum, ball, ball_type):
    RatingCalc.objects.create(user_id=user_id, check_sum=check_sum,
                              ball=ball, ball_type=ball_type)
