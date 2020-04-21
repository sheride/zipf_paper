#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 2020

@author: elijahsheridan
"""

import string
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np


def zipf_text_analysis(file):
    text = open(file, 'r')
    words = [str.lower(word.replace('\n', '').translate(
            str.maketrans('', '', string.punctuation)))
             for line in text.readlines() for word in line.split(' ')
             if word not in ['', '\n', 'TIME:', 'TRUMP:', 'SANDERS:']]
    words_dict = dict()

    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1

    keys = sorted(list(words_dict.keys()), key=lambda k: words_dict[k],
                  reverse=True)
    vals = list(words_dict.values())
    list.sort(vals, reverse=True)
    rank = [i+1 for i in range(len(vals))]

    log_rank = np.log(np.array(rank))
    log_vals = np.log(np.array(vals) / vals[0])

    settings = {'axes.labelsize': 16, 'lines.linewidth': 3,
                'lines.markersize': 7, 'xtick.labelsize': 14,
                'ytick.labelsize': 14}

    with plt.rc_context(settings):
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.scatter(log_rank, log_vals, label=file[:-4])
        ax.set_xlabel(r'$\ln(i)$')
        ax.set_ylabel(r'$\ln(p_i)$')
        plt.savefig(file[:-4], dpi=300, bbox_inches='tight')

    m, b, r, p, sigma = scipy.stats.linregress(log_rank, log_vals)

    m_err = sigma * np.sqrt(1 / np.sum((log_rank - np.mean(log_rank))**2))
    b_err = m_err * np.sqrt(np.sum(log_rank**2) / len(log_rank))

    info = {'len': len(words), 'keys': keys, 'vals': vals, 'logrank': log_rank,
            'logvals': log_vals, 'm': m, 'b': b, 'r': r, 'sigma': sigma,
            'm_err': m_err, 'b_err': b_err}

    return info


# TEXT A - Moby-Dick
m_info = zipf_text_analysis('mobydick.txt')
print('N = {}, r^2 = {}, m = {}'.format(m_info['len'], m_info['r']**2,
      m_info['m']))

# TEXT B - Ulysses
u_info = zipf_text_analysis('ulysses.txt')
print('N = {}, r^2 = {}, m = {}'.format(u_info['len'], u_info['r']**2,
      u_info['m']))

# TEXT C - President Trump TIME Interview
t_info = zipf_text_analysis('trump.txt')
print('N = {}, r^2 = {}, m = {}'.format(t_info['len'], t_info['r']**2,
      t_info['m']))

# TEXT D - Feynman Lectures
f_info = zipf_text_analysis('feynmann.txt')
print('N = {}, r^2 = {}, m = {}'.format(f_info['len'], f_info['r']**2,
      f_info['m']))

# TEXT E - Paradise Lost
p_info = zipf_text_analysis('parlost.txt')
print('N = {}, r^2 = {}, m = {}'.format(p_info['len'], p_info['r']**2,
      p_info['m']))

# TEXT F - Al Capone Interview
a_info = zipf_text_analysis('alcapone.txt')
print('N = {}, r^2 = {}, m = {}'.format(a_info['len'], a_info['r']**2,
      a_info['m']))
