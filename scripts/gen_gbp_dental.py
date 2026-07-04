"""Generate the dental-clinic GBP post (gbp-post-dental.png).

Same structure/spacing as the £/% stat post (gbp-post-2): big teal number,
one white line, one grey line, teal CTA button. Reuses gen_gbp_posts helpers.
"""
from gen_gbp_posts import (canvas, logo, center, cta_box, url, save,
                           f, BOLD, REG, WHITE, TEAL, GREY)


def post_dental():
    img, d = canvas()
    logo(d)
    center(d, 180, "£56,000", f(BOLD, 120), TEAL)
    center(d, 360, "lost to no-shows every year", f(REG, 28), WHITE)
    center(d, 425, "That's a full-time dental nurse's salary.", f(REG, 22), GREY)
    cta_box(d, 620, "We fix that. In one week.", f(BOLD, 24))
    url(d)
    save(img, "gbp-post-dental.png")


if __name__ == "__main__":
    post_dental()
